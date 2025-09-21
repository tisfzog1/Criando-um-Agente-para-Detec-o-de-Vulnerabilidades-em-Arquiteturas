document.getElementById("ameacasForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    const response = await fetch("http://localhost:8000/api/analise", {
        method: "POST",
        body: formData
    });

    const result = await response.json();
    const resultadoDiv = document.getElementById("resultado");

    // Tenta extrair o JSON do campo result
    let parsed = null;
    try {
        // Extrai o JSON de dentro do bloco de código, se houver
        const match = result.result.match(/```json\s*([\s\S]*?)```/);
        if (match) {
            parsed = JSON.parse(match[1]);
        } else {
            parsed = JSON.parse(result.result);
        }
    } catch (e) {
        resultadoDiv.textContent = "Erro ao processar resposta: " + e;
        return;
    }

    // Monta a tabela de ameaças (opcional)
    let html = "<h2>Modelo de Ameaças STRIDE</h2>";
    html += "<table border='1' style='border-collapse:collapse;'><tr><th>Tipo</th><th>Cenário</th><th>Impacto Potencial</th></tr>";
    parsed.threat_model.forEach(item => {
        html += `<tr><td>${item.stride_type}</td><td>${item.scenario}</td><td>${item.potential_impact}</td></tr>`;
    });
    html += "</table>";

    // Lista de sugestões de melhoria
    if (parsed.improvement_suggestions) {
        html += "<h3>Sugestões de Melhoria</h3><ul>";
        parsed.improvement_suggestions.forEach(sug => {
            html += `<li>${sug}</li>`;
        });
        html += "</ul>";
    }

    resultadoDiv.innerHTML = html;

    // --- Visualização com Cytoscape.js ---
    // Monta os nodes e edges a partir do modelo de ameaça
    const nodes = [
        { data: { id: 'app', label: 'Aplicação' } }
    ];
    const edges = [];

    parsed.threat_model.forEach((item, idx) => {
        const nodeId = `threat${idx}`;
        nodes.push({
            data: {
                id: nodeId,
                label: item.stride_type,
                scenario: item.scenario,
                impact: item.potential_impact
            }
        });
        edges.push({
            data: {
                source: 'app',
                target: nodeId
            }
        });
    });

    // Inicializa o Cytoscape
    cytoscape({
        container: document.getElementById('cy'),
        elements: {
            nodes: nodes,
            edges: edges
        },
        style: [
            {
                selector: 'node',
                style: {
                    'label': 'data(label)',
                    'text-wrap': 'wrap',
                    'text-max-width': 120,
                    'background-color': '#0074D9',
                    'color': '#fff',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'font-size': 12,
                    'width': 60,
                    'height': 60
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 2,
                    'line-color': '#ccc',
                    'target-arrow-color': '#ccc',
                    'target-arrow-shape': 'triangle'
                }
            }
        ],
        layout: {
            name: 'breadthfirst',
            directed: true,
            padding: 10
        }
    });
});