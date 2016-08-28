/**
 * Created by Jeffrey on 8/26/2016.
 */

var React = require('react');

module.exports = class Allies extends React.Component {
   render() {
        var allies_state=this.props.allies_state.map((ally_state) => {
            return(<Ally state={ally_state} />)
        })

       return (
           <div>
               <h1>Team</h1>
               <ul>
                   <li>
                   {this.props.my_state.name}
                   < br />
                   {this.props.my_state.hp}
                   < br />
                   {this.props.my_state.mp}
                   < br />
                   </li>
                   {allies_state}
               </ul>
           </div>
       )
   }
}

class Ally extends React.Component {
    render() {
        return (
            <li>
                {this.props.state.name}
                < br />
                {this.props.state.hp}
                < br />
                {this.props.state.mp}
            </li>
        )
    }
}