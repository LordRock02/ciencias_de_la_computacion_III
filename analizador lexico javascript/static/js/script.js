const textArea = document.getElementById('code')
const modalErrores = document.getElementById('modal-errores')
const modalTokens = document.getElementById('modal-tokens')



const analizarTexto = () => {
    let input = textArea.value
    console.log(input)
    fetch(`/analizar-lexico/${input}`, { method: 'POST' })
        .then(response => {
            return response.json()
        })
        .then(data => {
            alert(`resultado analisis ${JSON.stringify(data.result)}`)
            reporte(data.reporte.errores)
            tokens(data.reporte.tokens)
        })
}

const reporte = (errores) => {
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