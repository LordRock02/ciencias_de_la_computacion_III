const textArea = document.getElementById('code');
const modalErrores = document.getElementById('modal-errores');
const modalTokens = document.getElementById('modal-tokens');
const modalIntermediateCode = document.getElementById('modal-intermediate-code'); // Agregar un modal para el código intermedio

const analizarTexto = () => {
    let input = textArea.value;
    console.log(input);
    fetch(`/analizar-lexico/${encodeURIComponent(input)}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            alert(`resultado analisis ${JSON.stringify(data.result)}`);
            reporteLexico(data.reporte.errores);
            tokens(data.reporte.tokens);
            intermediateCode(data.intermediate_code); // Mostrar el código intermedio
        })
        .catch(error => {
            console.error('Error:', error);
        });
};

const reporte = (errores) => {
    console.log(errores);
    let table = document.createElement('table');
    table.innerHTML = `
    <thead>
        <tr>
            <th>#</th>
            <th>Error</th>
        </tr>
    </thead>
    <tbody>
        ${errores.map((error, index) => `
            <tr>
                <td>${index + 1}</td>
                <td>${error}</td>
            </tr>
        `).join('')}
    </tbody>
    `;
    modalErrores.innerHTML = '';
    modalErrores.appendChild(table);
};

const tokens = (tokens) => {
    console.log(tokens);
    let table = document.createElement('table');
    table.innerHTML = `
    <thead>
        <tr>
            <th>#</th>
            <th>Token</th>
        </tr>
    </thead>
    <tbody>
        ${tokens.map((token, index) => `
            <tr>
                <td>${index + 1}</td>
                <td>${token}</td>
            </tr>
        `).join('')}
    </tbody>
    `;
    modalTokens.innerHTML = '';
    modalTokens.appendChild(table);
};

const intermediateCode = (code) => {
    console.log(code);
    let table = document.createElement('table');
    table.innerHTML = `
    <thead>
        <tr>
            <th>#</th>
            <th>Intermediate Code</th>
        </tr>
    </thead>
    <tbody>
        ${code.map((instr, index) => `
            <tr>
                <td>${index + 1}</td>
                <td>${JSON.stringify(instr)}</td>
            </tr>
        `).join('')}
    </tbody>
    `;
    modalIntermediateCode.innerHTML = '';
    modalIntermediateCode.appendChild(table);
};
