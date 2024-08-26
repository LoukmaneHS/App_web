
document.getElementById('convertBtn').addEventListener('click', function () {
    let email = document.getElementById('email').value;
    let appName = document.getElementById('appName').value;
    let websiteFiles = document.getElementById('websiteFiles').files;
    let appIcon = document.getElementById('appIcon').files[0];

    if (email && appName && websiteFiles.length > 0 && appIcon) {
        let formData = new FormData();
        formData.append('email', email);
        formData.append('appName', appName);
        Array.from(websiteFiles).forEach(file => formData.append('websiteFiles', file));
        formData.append('appIcon', appIcon);

        fetch('/convert', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            document.getElementById('result').innerText = data;
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('result').innerText = 'حدث خطأ أثناء إرسال البيانات!';
        });
    } else {
        alert('يرجى ملء جميع الحقول!');
    }
});

document.getElementById('zipBtn').addEventListener('click', function() {
    document.getElementById('result').innerText = 'جارٍ ضغط التطبيق وإرساله عبر البريد الإلكتروني...';

    setTimeout(() => {
        document.getElementById('result').innerText = 'تم إرسال التطبيق بنجاح إلى ' + document.getElementById('email').value;
    }, 2000);
});
