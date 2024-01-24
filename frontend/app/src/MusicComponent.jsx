import React, {useEffect} from 'react';
import * as music21 from 'music21j'; // Importing all exports as music21

function MusicComponent(){
    useEffect(() => {
        // Fetch your MXL file or load it in some way
        const mxlFile = "";

        const score = music21.converter.parse(musicXmlData);
        //
        // const scoreContainer = document.getElementById('score-container');
        // score.appendNewDOM(scoreContainer);

        // music21.converter.parse(mxlFile)
        //     .then(score => {
        //
        //         console.log("score:", score)
        //         const scoreContainer = document.getElementById('score-container');
        //         scoreContainer.innerHTML = '';
        //         score.appendNewDOM(scoreContainer);
        //     })
        //     .catch(error => {
        //         console.error('Error loading the MXL file:', error);
        //     });
    }, []); // Run the effect only once when the component mounts

    return (
        <div id="score-container">
        </div>
    );
};

export default MusicComponent;
