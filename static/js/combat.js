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
            character_state:null, combatants_state:[], messages:[], skills:[]
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
                this.setState({skills: data.objects});
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
            console.log(this.state.character_state);

        });

        //state for all characters
        socket.on('general combat state', (combat_state) => {
            //this.setState({combatants_state:combat_state});
            //console.log(this.state.combatants_state);
        });
    }

    render() {
    return (
        <Grid>
            <Row>
                <Col lg={2}>
                    <Status />
                </Col>
                <Col lg={7}>
                    <Row>
                        <Col lg={12}>
                            <Display />
                        </Col>
                    </Row>
                    <Row>
                        <Col lg={8}>
                            <Skills skills={this.state.skills}/>
                        </Col>
                        <Col lg={4}>
                            <Targets/>
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

class Status extends React.Component {
   render() {
       return (
           <div>
               <h1>Status</h1>
               <ul>
                   <li>Larken</li>
                   <li>Ilfantz</li>
                   <li>Vimilikirti</li>
               </ul>
           </div>
       )
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

class Skills extends React.Component {
    render() {
        var my_skills = this.props.skills.map((skill) => {
            return (
                <div key={skill.id}>
                    {skill.name}
                    <br />
                    {skill.description}
                </div>
            );

        });

        return (
            <div>
                <h1>Skills</h1>
                {my_skills}
            </div>
        );
    }
}

class Targets extends React.Component {
    render() {
        return (
            <h1>Targets</h1>
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