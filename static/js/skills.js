/**
 * Created by Jeffrey on 8/26/2016.
 */

import React from "react";
import {observer, action} from "mobx-react";

export const Skills = observer(({skills_store}) => {
    let my_skills = skills_store.skill_ids.map((skill_id) => {
        let skill = skills_store.skills[skill_id];
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
});

const SkillDisplay = observer(({skill}) => {
    function select_skill(e) {
        skill.select();
    }
    let css_class = skill.selected ? "grey" : "";
    let skill_text = skill.name + " " + skill.condition;

    let skill_component;
    if(skill.valid) {
        skill_component = <div className={css_class} onClick={select_skill}>{skill_text}</div>
    }
    else {
        skill_component = <div className="greyed-text">{skill_text}</div>
    }

    return (
        <li>
            {skill_component}
        </li>
    )
});