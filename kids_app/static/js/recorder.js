document
    .getElementById("startRecording")
    .addEventListener("click", initFunction);

let isRecording = document.getElementById("isRecording");

function initFunction() {
    // Display recording
    async function getUserMedia(constraints) {
        if (window.navigator.mediaDevices) {
            return window.navigator.mediaDevices.getUserMedia(constraints);
        }

        let legacyApi =
            navigator.getUserMedia ||
            navigator.webkitGetUserMedia ||
            navigator.mozGetUserMedia ||
            navigator.msGetUserMedia;

        if (legacyApi) {
            return new Promise(function (resolve, reject) {
                legacyApi.bind(window.navigator)(constraints, resolve, reject);
            });
        } else {
            alert("user api not supported");
        }
    }

    isRecording.className = ""

    //

    let audioChunks = [];
    let rec;

    function saveBlob(blob, fileName) {
        var a = document.createElement("a");
        document.body.appendChild(a);
        a.style = "display: none";

        var url = window.URL.createObjectURL(blob);
        a.href = url;
        a.download = fileName;
        a.click();
        window.URL.revokeObjectURL(url);
    }

    function handlerFunction(stream) {
        rec = new MediaRecorder(stream);
        rec.start();
        rec.ondataavailable = (e) => {
            audioChunks.push(e.data);
        };
    }

    function startusingBrowserMicrophone(boolean) {
        getUserMedia({audio: boolean}).then((stream) => {
            handlerFunction(stream);
        });
    }

    startusingBrowserMicrophone(true);

    // Stoping handler
    document.getElementById("stopRecording").addEventListener("click", (e) => {
        rec.stop();
        let blob = new Blob(audioChunks, {type: "audio/wav"})
        let file = new File([blob], "audio.wav", {type: "audio/wav"});
        let container = new DataTransfer();
        if (file.size > 0) {
            container.items.add(file);
            console.log(container)
            document.querySelector('#id_file').files = container.files;
            isRecording.className = "hidden";

        }


    });
}
