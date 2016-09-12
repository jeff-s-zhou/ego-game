/**
 * Created by Jeffrey on 9/6/2016.
 */

import React from 'react'
import {observer} from "mobx-react";



const TurnBar = observer((props) => {
    //if not set yet, then false. If set, then check if it's true or false
    var up_to_bat = props.combatants_store.me != null ? props.combatants_store.me.up_to_bat : false;
    if(up_to_bat) {
        var elem = document.getElementById("turn-fill");
        var width = 500;
        var id = setInterval(frame, 10);
        function frame() {
            if (width <= 0) {
                clearInterval(id);
            } else {
                width--;
                var pixel_width = width/5;
                elem.style.width = pixel_width + '%';
            }
        }
    }
    return (
        <div id="turn-bar">
            <div id="turn-fill" className="turn-bar-elements whitebg"></div>
            <div className="turn-bar-elements blackbg"></div>
            <div className="turn-bar-elements makeblack"></div>
            <span id="turn-bar-text">{up_to_bat ? "YOUR TURN" : "WAITING"}</span>
        </div>
    );
});

module.exports =  TurnBar;