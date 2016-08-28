/**
 * Created by Jeffrey on 8/26/2016.
 */

import React from 'react'
import {observer} from "mobx-react";

@observer
class Skills extends React.Component {
    render() {
        var result_list = [];

        for(var key in this.props.app_state.skills){
            var skill = this.props.app_state.skills[key];
            result_list.push(skill)
        }

        var my_skills = result_list.map((skill) => {
            return (<Skill key={skill.id} skill={skill} caster_id={3}/>)
        });

        return (
            <div>
                <h1>Skills</h1>
                {my_skills}
            </div>
        );
    }
}

@observer
class Skill extends React.Component {
    handleSubmit(e) {
        //socket.emit("turn input", {caster_id: caster_id, skill_id: skill_id, target_id: target_id});
        console.log("handling submit")
    }

    render() {
        var skill_activate;
        if(this.props.skill.valid) {
            skill_activate = <div onClick={this.handleSubmit.bind(this)}>Click here</div>
        }
        else {
            skill_activate = 'ON COOLDOWN"'
        }

        return (
            <div>
                {this.props.skill.name}
                <br />
                {this.props.skill.description}
                <br />
                {this.props.skill.cooldown}
                <br />
                {skill_activate}
            </div>
        )
    }
}

module.exports = Skills;