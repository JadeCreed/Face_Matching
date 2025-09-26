// Preview uploaded photo
function previewImage(inputId, previewId) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);
    preview.innerHTML = '';
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.style.maxWidth = '100px';
            img.style.maxHeight = '100px';
            preview.appendChild(img);
        }
        reader.readAsDataURL(input.files[0]);
    }
}

document.getElementById('studentPicture')?.addEventListener('change', function() {
    previewImage('studentPicture', 'previewStudent');
});

document.getElementById('studentSignature')?.addEventListener('change', function() {
    previewImage('studentSignature', 'previewSignature');
});

// Auto-submit student list photo uploads
document.getElementById('photosInput')?.addEventListener('change', function() {
    document.getElementById('uploadPhotosForm').submit();
});



document.querySelectorAll('.sortable').forEach(th => {
  th.addEventListener('mouseenter', () => {
    const dropdown = th.querySelector('.sort-dropdown');
    if(dropdown) dropdown.style.display = 'block';
  });
  th.addEventListener('mouseleave', () => {
    const dropdown = th.querySelector('.sort-dropdown');
    if(dropdown) dropdown.style.display = 'none';
  });
});


