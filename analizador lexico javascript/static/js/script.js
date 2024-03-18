const textArea = document.getElementById('code')

const analizarTexto = () => {
    let input = textArea.value
    console.log(input)
    fetch(`/analizar-lexico/${input}`, {method:'POST'})
        .then(response => {
            return response.json()
        })
        .then(data =>{
            alert(`resultado analisis ${data.result}`)
        })
}