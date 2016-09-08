/**
 * Created by Jeffrey on 8/26/2016.
 */

import React from 'react'
import {observer} from "mobx-react";

@observer
class Targets extends React.Component {

    render() {
        var targets = this.props.combatants_store.get_targets("fake_data").map((target) => {
            return(<Target skills_store={this.props.skills_store}
                           target={target}
                           me={this.props.combatants_store.me}
                           key={target.id}/>)
        });

        return (
            <div>
            <h2>Targets</h2>
            <ul>
            {targets}
            </ul>
            </div>
        )
    }
}

@observer
class Target extends React.Component {
    select_target(e) {
        if(this.props.target.selected) {
            this.props.skills_store.cast(this.props.me, this.props.target);
        }
        else {
            this.props.target.select();
        }
    }

    render() {
        var css_class = this.props.target.selected ? "grey" : "";
        return (
            <li className={css_class} onClick={this.select_target.bind(this)}>
                {this.props.target.name}
            </li>
        );
    }
}

module.exports = Targets;
