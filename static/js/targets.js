/**
 * Created by Jeffrey on 8/26/2016.
 */

import React from 'react'
import {observer} from "mobx-react";
import {reaction} from "mobx";
import target_types from "./types";

@observer
class Targets extends React.Component {

    render() {
        var t_types;
        if(this.props.skills_store.selected != null){
            t_types = this.props.skills_store.selected.valid_targets;
        }
        else {
            t_types = [target_types.single_enemy];
        }
        var targets = this.props.combatants_store.get_targets(t_types).map((target) => {
            return(<Target skills_store={this.props.skills_store}
                           target={target}
                           me={this.props.combatants_store.me}
                           key={target.id}/>)
        });

        return (
            <div>
            <h2>TARGETS</h2>
            <ul>
            {targets}
            </ul>
            </div>
        )
    }
}

@observer
class Target extends React.Component {
    constructor(props) {
        super(props);
        this.disposer = reaction(() => props.target.hp, hp => {
            //TODO: abstract to handle healing
            var final_health_width = Math.round((hp / props.target.max_hp) * 200);
            var elem = document.getElementById(props.target.id + "-health-fill");
            var width = elem.style.width;
            if (width == "") {
                //base case
                width = 200;
                elem.style.width = width/2 + '%';
            }
            else {
                width = parseInt(width.slice(0, width.length - 1)) * 2;
                var id = setInterval(frame, 10);
                var sign = (final_health_width - width)/Math.abs(final_health_width - width);
                function frame() {
                    if (width == final_health_width) {
                        clearInterval(id);
                    } else {
                        width += sign;
                        elem.style.width = width/2 + '%';
                    }
                }
            }
        });
    }



    select_target(e) {
        if(this.props.target.selected) {
            if(this.props.me.up_to_bat){
                this.props.skills_store.cast(this.props.me, this.props.target);
            }
            else{
                var elem = document.getElementById("turn-fill");
                var id = setInterval(frame, 120);
                var flash_times = 7;
                function frame() {
                    if (flash_times <= 0) {
                        clearInterval(id);
                    } else {
                        flash_times--;
                        elem.style.width = (flash_times % 2 ? 0 : 100) + "%";
                    }
                }
            }
        }
        else {
            this.props.target.select();
        }
    }

    render() {
        var bar_id = this.props.target.id + "-health-fill";
        var css_class = this.props.target.selected ? "grey" : "";
        return (
            <li className={css_class} onClick={this.select_target.bind(this)}>
                {this.props.target.name}
                < br />
                <div id="ally-health-bar">
                    <div id={bar_id} className="ally-health-bar-elements whitebg"></div>
                    <div className="ally-health-bar-elements blackbg"></div>
                    <div className="ally-health-bar-elements makeblack"></div>
                </div>
            </li>
        );
    }
}

module.exports = Targets;
