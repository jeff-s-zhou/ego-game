/**
 * Created by Jeffrey on 8/26/2016.
 */

import React from 'react'
import {observer} from "mobx-react";

@observer
class Targets extends React.Component {

    render() {
        var targets = this.props.combatants_store.get_targets("fake_data").map((target) => {
            return(<Target target={target} my_character_store={this.props.my_character_store} key={target.id}/>)
        });

        return (
            <div>
            <h1>Targets</h1>
            {targets}
            </div>
        )
    }
}

@observer
class Target extends React.Component {
    select_target(e) {
        this.props.my_character_store.cast_selected_on(this.props.target.id);
    }

    render() {
        return (
            <li onClick={this.select_target.bind(this)}>
                {this.props.target.name}
            </li>
        );
    }
}

module.exports = Targets;
