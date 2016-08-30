/**
 * Created by Jeffrey on 8/26/2016.
 */

var React = require('react');
import {observer} from "mobx-react";

@observer
class Allies extends React.Component {
   render() {
        var allies_state=this.props.allies_store.ally_ids.map((ally_id) => {
            return(<Ally ally={this.props.allies_store.allies[ally_id]} />)
        });

       return (
           <div>
               <h1>Team</h1>
               <ul>
                   <li>
                   {this.props.my_character_store.name}
                   < br />
                   {this.props.my_character_store.hp}
                   < br />
                   {this.props.my_character_store.mp}
                   < br />
                   </li>
                   {allies_state}
               </ul>
           </div>
       )
   }
}

@observer
class Ally extends React.Component {
    render() {
        return (
            <li>
                {this.props.ally.name}
                < br />
                {this.props.ally.hp}
                < br />
                {this.props.ally.mp}
            </li>
        )
    }
}

module.exports = Allies;