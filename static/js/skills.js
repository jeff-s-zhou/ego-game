/**
 * Created by Jeffrey on 8/26/2016.
 */

import React from 'react'
import {observer} from "mobx-react";

@observer
class Skills extends React.Component {
    render() {
        var my_skills = this.props.skills_store.skill_ids.map((skill_id) => {
            var skill = this.props.skills_store.skills[skill_id];
            console.log("it's happenninnnggg");
            return (<Skill key={skill_id} skill={skill} caster_id={3}/>)
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
                {this.props.skill.condition}
                <br />
                {skill_activate}
            </div>
        )
    }
}

module.exports = Skills;