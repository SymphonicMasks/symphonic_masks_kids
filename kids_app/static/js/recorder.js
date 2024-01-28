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

    isRecording.textContent = "Recording...";
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
            if (rec.state == "inactive") {
                let blob = new Blob(audioChunks, {type: "audio/wav"})

                var xhr = new XMLHttpRequest();
                xhr.onload = function (e) {
                    if (this.readyState === 4) {
                        console.log("Server returned: ", e.target.responseText);
                    }
                };
                var fd = new FormData();
                fd.append("file", blob, "audio");
                xhr.open("POST", "/upload/recording/", true);
                xhr.send(fd);
                console.log(blob);
                console.log(f);
                document.getElementById("audioElement").src = URL.createObjectURL(blob);
            }
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
        isRecording.textContent = "Click play button to start listening";
    });
}
