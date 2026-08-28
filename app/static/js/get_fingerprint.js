import FingerprintJS from './fingerprint_v3.js';

document.addEventListener("DOMContentLoaded", () => {
    FingerprintJS.load()
        .then(fp => fp.get())
        .then(result => {
            const inputFp = document.getElementById('fingerprint_id');
            if (inputFp) {
                inputFp.value = result.visitorId;
            }
        })
        .catch(_ => console.error(""));
});