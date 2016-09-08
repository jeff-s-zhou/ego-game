/**
 * Created by Jeffrey on 8/26/2016.
 */

var React = require('react');
import {observer} from "mobx-react";

@observer
class Allies extends React.Component {
   render() {
        var allies= this.props.combatants_store.ally_ids.map((ally_id) => {
            return(<Ally ally={this.props.combatants_store.allies[ally_id]} key={ally_id} />)
        });
       var me;
       if(this.props.combatants_store.me != null) {
           me = <Ally ally={this.props.combatants_store.me}/>
       }


       return (
           <div>
               <h2>Team</h2>
               <ul>
                   {me}
                   {allies}
               </ul>
           </div>
       )
   }
}

@observer
class Ally extends React.Component {
    render() {
        var bar_id = this.props.ally.id + "-health-fill";
        return (
            <li>
                {this.props.ally.name}
                < br />
                <div id="ally-health-bar">
                    <div id={bar_id} className="ally-health-bar-elements whitebg"></div>
                    <div className="ally-health-bar-elements blackbg"></div>
                    <div className="ally-health-bar-elements makeblack"></div>
                    <span id="ally-health-bar-text">{this.props.ally.hp + "/" + this.props.ally.max_hp}</span>
                </div>

            </li>
        )
    }
}

module.exports = Allies;