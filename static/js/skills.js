/**
 * Created by Jeffrey on 8/26/2016.
 */

import React from 'react'
import {observer, action} from "mobx-react";

@observer
class Skills extends React.Component {
    render() {
        var my_skills = this.props.skills_store.skill_ids.map((skill_id) => {
            var skill = this.props.skills_store.skills[skill_id];
            return (<SkillDisplay key={skill_id} skill={skill}/>)
        });

        return (
            <div>
                <h2>Skills</h2>
                {my_skills}
            </div>
        );
    }
}

@observer
class SkillDisplay extends React.Component {
    select_skill(e) {
        this.props.skill.select();
    }

    render() {
        var skill_activate;
        if(this.props.skill.valid) {
            skill_activate = <div onClick={this.select_skill.bind(this)}>Click here</div>
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