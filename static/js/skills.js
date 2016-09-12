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
                <h2>SKILLS</h2>
                <ul>
                {my_skills}
                </ul>
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
        var css_class = this.props.skill.selected ? "grey" : "";
        var skill_text = this.props.skill.name + " " + this.props.skill.condition;
        var skill;
        if(this.props.skill.valid) {
            skill = <div className={css_class} onClick={this.select_skill.bind(this)}>{skill_text}</div>
        }
        else {
            skill = <div className="greyed-text">{skill_text}</div>
        }

        return (
            <li>
                {skill}
            </li>
        )
    }
}

module.exports = Skills;