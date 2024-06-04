const textArea = document.getElementById('code')
const modalErrores = document.getElementById('modal-errores')
const modalTokens = document.getElementById('modal-tokens')
const modalSintaxis = document.getElementById('modal-sintaxis')
const modalSemantico = document.getElementById('modal-semantico')



const analizarTexto = () => {
    let input = textArea.value
    console.log(input)
    fetch(`/analizar-lexico/${input}`, { method: 'POST' })
        .then(response => {
            return response.json()
        })
        .then(data => {
            alert(`resultado analisis ${JSON.stringify(data.result)}`)
            reporteLexico(data.reporteLexico.errores)
            reporteSintactico(data.reporteSintactico)
            reporteSemantico(data.reporteSemantico)
            tokens(data.reporteLexico.tokens)
        })
}

const reporteLexico = (errores) => {
    console.log(errores)
    let table = document.createElement('table')
    table.innerHTML = `
    <thead>
        <tr>
            <th>#</th>
            <th>error</th>
        </tr>
        <tbody>
        ${errores.map((error, index) => `
            <tr>
                <td>${index + 1}</td>
                <td>${error}</td>
            </tr>
        `).join('')}
        </tbody>
    </thead>
    `
    modalErrores.innerHTML = ''
    modalErrores.appendChild(table)
}
const reporteSintactico = (errores) => {
    console.log(`errrores sintacticos ${errores}`)
    let table = document.createElement('table')
    table.innerHTML = `
    <thead>
        <tr>
            <th>#</th>
            <th>error</th>
        </tr>
        <tbody>
        ${errores.map((error, index) => `
            <tr>
                <td>${index + 1}</td>
                <td>${error}</td>
            </tr>
        `).join('')}
        </tbody>
    </thead>
    `
    modalSintaxis.innerHTML = ''
    modalSintaxis.appendChild(table)
}

const reporteSemantico = (errores) => {
    console.log(`errrores semanticos ${errores}`)
    let table = document.createElement('table')
    table.innerHTML = `
    <thead>
        <tr>
            <th>#</th>
            <th>error</th>
        </tr>
        <tbody>
        ${errores.map((error, index) => `
            <tr>
                <td>${index + 1}</td>
                <td>${error}</td>
            </tr>
        `).join('')}
        </tbody>
    </thead>
    `
    modalSemantico.innerHTML = ''
    modalSemantico.appendChild(table)
}

const tokens = (tokens) => {
    console.log(tokens)
    let table = document.createElement('table')
    table.innerHTML = `
    <thead>
        <tr>
            <th>#</th>
            <th>token</th>
        </tr>
        <tbody>
        ${tokens.map((error, index) => `
            <tr>
                <td>${index + 1}</td>
                <td>${error}</td>
            </tr>
        `).join('')}
        </tbody>
    </thead>
    `
    modalTokens.innerHTML = ''
    modalTokens.appendChild(table)
}