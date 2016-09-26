/**
 * Created by Jeffrey on 9/6/2016.
 */

import React from "react";
import {observer} from "mobx-react";

export const TurnBar = observer(({allies_store}) => {
    //if not set yet, then false. If set, then check if it's true or false
    let up_to_bat = false;
    if (allies_store.me != null) {
        up_to_bat =  allies_store.me.up_to_bat
    }
    if(up_to_bat) {
        let elem = document.getElementById("turn-fill");
        let width = 500;
        let id = setInterval(frame, 10);
        function frame() {
            if (width <= 0) {
                clearInterval(id);
            } else {
                width--;
                let pixel_width = width/5;
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
