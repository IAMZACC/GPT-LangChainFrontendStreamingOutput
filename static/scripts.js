document.getElementById('tripForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    var formData = new FormData(this);

    fetch('/search', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').textContent = data.result;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});