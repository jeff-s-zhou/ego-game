/**
 * Created by Jeffrey on 7/4/2016.
 */

var React = require('react');
var JQuery = require('jquery');
var Grid = require('react-bootstrap/lib/Grid');
var Row = require('react-bootstrap/lib/Row');
var Col = require('react-bootstrap/lib/Col');

var socket = require('socket.io-client')('http://' + document.domain + ':' + location.port + '/test');

module.exports = class Home extends React.Component{

    constructor(props) {
        super(props);
        this.state =  {
            character_state:{name:'', id:0, hp:0, mana:0, active_skills:[], statuses:[]},
            allies_state:[],
            enemies_state:[],
            messages:[],
            skills:{}
        }
    }

    //TODO: get actual skill based on character id, and not spoofing
    loadSkillsFromServer() {
        JQuery.ajax({
            url: ("/api/skill"),
            contentType: "application/json",
            dataType: "json",
            cache: false,
            success: (data) => {
                var my_skills = {};
                data.objects.map((skill) => {
                    my_skills[skill.id] = skill
                });
                this.setState(
                    {skills: my_skills}
                );
            },
            error: (xhr, status, err) => {
                console.error("api/ego", status, err.toString());
            }
        });
    }

    componentDidMount() {
        this.loadSkillsFromServer();

        socket.on('connect', () => {console.log("connected");});

        //chat
        socket.on('chat message', (msg) => {
            JQuery('#messages').append(JQuery('<li>').text(msg));
        });

        socket.on('combat start', (start) => {
            console.log(start)
        });


        socket.on('current turn', (character_name) => {
            //console.log(character_name)
        });

        //state for just the character
        socket.on('my combat state', (my_combat_state) => {
            this.setState({character_state:my_combat_state});

            var old_skills = this.state.skills;
            my_combat_state.active_skills.map((skill) => {
                old_skills[skill.id].cooldown = skill.cooldown
            });
            this.setState({skills: old_skills});
        });

        //state for my team
        socket.on('allies state', (allies_state) => {
            this.setState({allies_state:allies_state});
            console.log(allies_state);
        });

        //state for enemies
        socket.on('enemy state', (enemy_state) => {
            this.setState({enemies_state:enemies_State});
            console.log(enemy_state);
        });
    }

    render() {
    return (
        <Grid>
            <Row>
                <Col lg={2}>
                    <States my_state={this.state.character_state} allies_state={this.state.allies_state}/>
                </Col>
                <Col lg={7}>
                    <Row>
                        <Col lg={12}>
                            <Display />
                        </Col>
                    </Row>
                    <Row>
                        <Col lg={8}>
                            <Skills skills={this.state.skills} caster_id={this.state.character_state.id}/>
                        </Col>
                        <Col lg={4}>
                            <Targets enemies_state={this.state.enemies_state}/>
                        </Col>
                    </Row>
                </Col>
                <Col lg={3}>
                    <ChatForm />
                </Col>
            </Row>
        </Grid>
    )
  }
}

class States extends React.Component {
   render() {
        var allies_state=this.props.allies_state.map((ally) => {
            return(<State/>)
        })

       return (
           <div>
               <h1>Team</h1>
               <ul>
                   <li>Larken</li>
                   {allies_state}
               </ul>
           </div>
       )
   }
}

class State extends React.Component {

}


class Skills extends React.Component {
    render() {
        var result_list = [];

        for(var key in this.props.skills){
            var skill = this.props.skills[key];
            result_list.push(skill)
        }

        var my_skills = result_list.map((skill) => {
            return (<Skill key={skill.id} skill={skill} caster_id={this.props.caster_id}/>)
        });

        return (
            <div>
                <h1>Skills</h1>
                {my_skills}
            </div>
        );
    }
}

class Skill extends React.Component {
    handleSubmit(e) {
        console.log("handle submit's this is " + this);
        var caster_id = 3;
        var skill_id = 8
        var target_id = 2;
        socket.emit("turn input", {caster_id: caster_id, skill_id: skill_id, target_id: target_id});
        console.log("handling submit")
    }

    render() {
        var skill_activate;
        if(this.props.skill.valid) {
            skill_activate = <div onClick={this.handleSubmit.bind(this)}>Click here</div>
        }
        else {
            skill_activate = 'ON COOLDOWN"'
        }

        return (
            <div>
                {this.props.skill.name}
                <br />
                {this.props.skill.description}
                <br />
                {this.props.skill.cooldown}
                <br />
                {skill_activate}
            </div>
        )
    }
}

class Targets extends React.Component {
    render() {
        return (
            <h1>Targets</h1>
        );
    }
}


class Display extends React.Component{
    render() {
        return (
            <div id="combat">
                <h1>Combat</h1>
                <ul>
                    <li>Millia begins FOCUSING.</li>

                    <li>Khazarak uses MEZZO SLASH on Ilfantz, dealing 12 DAMAGE.</li>

                    <li>Ilfantz is heavily wounded!</li>

                    <li>Vimilikirti uses SHADOW STUTTER, dealing 15 DAMAGE to ALL ENEMIES!</li>

                    <li>Vimilikirti is now EVASIVE for 2 TURNS.</li>

                    <li>YOU are going!</li>

                    <li>NEXT: Ilfantz, Sinistr, Mazara, Verit</li>
                </ul>
            </div>
        );
    }
}

class ChatForm extends React.Component {
    handleSubmit(e) {
        console.log("handling Submit");
        socket.emit('chat message', JQuery('#m').val());
        JQuery('#m').val('');
    }
    render() {
        return (
        <div className="Home">
        <ul id="messages"></ul>
        <form action="" onSubmit={this.handleSubmit}>
          <input id="m" autoComplete="off" /><button>Send</button>
        </form>
        </div>
        );
    }
}