/**
 * Created by Jeffrey on 8/26/2016.
 */

import React from 'react'
import {observer} from "mobx-react";

@observer
class Targets extends React.Component {

    render() {
        var targets = this.props.combatants_store.get_targets("fake_data").map((target) => {
            return(<Target target={target} key={target.id}/>)
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
    render() {
        return (
            <li>
                {this.props.target.name}
            </li>
        );
    }
}

module.exports = Targets;
