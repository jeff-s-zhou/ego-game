/**
 * Created by Jeffrey on 8/26/2016.
 */

var React = require('react');
import {reaction} from "mobx";
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
               <h2>TEAM</h2>
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
    constructor(props){
        super(props);
        this.disposer = reaction(() => props.ally.hp, hp => {
            //TODO: abstract to handle healing
            var final_health_width = Math.round((hp / props.ally.max_hp) * 200);
            var elem = document.getElementById(props.ally.id + "-health-fill");
            var width = elem.style.width;
            if (width == "") {
                //base case
                width = 200;
                elem.style.width = width/2 + '%';
            }
            else {
                width = parseInt(width.slice(0, width.length - 1)) * 2;
                var id = setInterval(frame, 10);
                var sign = (final_health_width - width)/Math.abs(final_health_width - width);
                function frame() {
                    if (width == final_health_width) {
                        clearInterval(id);
                    } else {
                        width += sign;
                        elem.style.width = width/2 + '%';
                    }
                }
            }
        });

    }

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