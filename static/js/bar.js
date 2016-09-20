/**
 * Created by Jeffrey on 9/19/2016.
 */
import React from "react";

export class Bar extends React.Component {
    constructor(props){
        super(props);
        this.state = {bar_width: props.width};
    }

    componentWillReceiveProps(next_props) {
        let final_health_width = next_props.width;
        let id = setInterval(frame, 10);
        let sign = (final_health_width - this.state.bar_width)/Math.abs(final_health_width - this.state.bar_width);
        let self = this;
        function frame() {
            if (self.state.bar_width == final_health_width) {
                console.log("cleared");
                clearInterval(id);
            } else {
                self.setState({bar_width: self.state.bar_width + sign});
            }
        }
    }

    flicker_border() {
        /*let id = setInterval(frame, 120);
        let flash_times = 7;
        function frame() {
            if (flash_times <= 0) {
                clearInterval(id);
            } else {
                flash_times--;
                elem.style.width = (flash_times % 2 ? 0 : 100) + "%";
            }
        }*/
    }

    render() {

        return (
            <div id="ally-health-bar">
                <div style={{width: this.state.bar_width + "%"}} className="ally-health-bar-elements whitebg"></div>
                <div className="ally-health-bar-elements blackbg"></div>
                <div className="ally-health-bar-elements makeblack"></div>
                <span id="ally-health-bar-text">{this.props.text}</span>
            </div>
        )
    }
}

