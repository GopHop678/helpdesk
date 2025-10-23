document.addEventListener('DOMContentLoaded', function() {
    const filesInputField = document.getElementById('files-input');
    const filesWrapper = document.querySelector('.files-list');
    let files = [];

    filesInputField.addEventListener('change', function() {
        let filesString = ''
        const inputFiles = filesInputField.files;

        for (const file of inputFiles) {
            if (!files.includes(file)) {
                files.push(file);
            }
        }

        for (const file of files) {
            filesString += file.name + ' ';
        }
        filesWrapper.textContent = filesString;
        inputFiles.files = files;
    })

});