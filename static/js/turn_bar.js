/**
 * Created by Jeffrey on 9/6/2016.
 */

import React from 'react'
import {observer} from "mobx-react";



const TurnBar = observer((props) => {
    //if not set yet, then false. If set, then check if it's true or false
    var up_to_bat = props.combatants_store.me != null ? props.combatants_store.me.up_to_bat : false;
    var bar_text = up_to_bat ? "YOUR TURN" : "WAITING" ;
    function move() {
        var elem = document.getElementById("whitebg");
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
    if(up_to_bat) {
        move();
    }
    return (
        <div id="bar">
            <div id="whitebg" className="bar-elements"></div>
            <div id="blackbg" className="bar-elements"></div>
            <div id="makeblack" className="bar-elements"></div>
            <span>{bar_text}</span>
        </div>
    );
});

module.exports =  TurnBar;