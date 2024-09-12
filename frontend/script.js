document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/convert_and_merge', true);
    xhr.responseType = 'blob'; // To handle the file download
  
    // Show waiting animation
    console.log('show animation')
    var waitingAnimation = document.querySelector('.waiting-animation');
    waitingAnimation.style.display = 'block';
  
    xhr.onload = function() {
        console.log('crazy')
      if (xhr.status === 200) {
        console.log('hide animation')
        var a = document.createElement('a');
        a.href = window.URL.createObjectURL(xhr.response);
        a.download = 'merged_output.pdf';
        a.click();
        waitingAnimation.style.display = 'none';
      } else {
        document.getElementById('result').textContent = 'An error occurred while processing the files.';
        waitingAnimation.style.display = 'none';
      }
    };
  
    xhr.send(formData);
  });