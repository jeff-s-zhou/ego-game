/**
 * Created by Jeffrey on 8/26/2016.
 */

import React from 'react'
import {observer} from "mobx-react";

@observer
class Targets extends React.Component {

    render() {
        var targets = this.props.enemies_state.map((enemy) => {
            return(<Target enemy={enemy} key={enemy.id}/>)
        })

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
                {this.props.enemy.name}
            </li>
        );
    }
}

module.exports = Targets;
