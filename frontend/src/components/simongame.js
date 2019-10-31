import 'bootstrap/dist/css/bootstrap.min.css';
import $ from 'jquery';
import Popper from 'popper.js';
import 'bootstrap/dist/js/bootstrap.bundle.min';
import React from "react";
import {getGameId, ajax} from "../utils";
import Simon from "./simon";
import Players from "./players";
import Sequence from "./sequence";
import BackBtn from "./back";
import Modal from "../components/modal";

let STEPS = 5;

export default class SimonGame extends React.Component {
    constructor(){
        super();
        this.state = {game:{status:"loading", sequence:[]}, user:{name:"", status:""}, players:[]}
    }

    componentDidMount() {
        this.gameLoop();
    }

    UNSAFE_componentWillUpdate(nextProps, nextState) {
        if ((nextState.game.status == "won" || nextState.game.status == "failed") && 
            this.state.game.status !== "loading") {
                $("#myModal").modal();
            }
        // if (nextState.players.length == STEPS) {
        //     this.setState({
        //         game: {
        //             ...this.state.game,
        //             status: "full",
        //         }
        //     })
        // }
    }

    gameLoop(){
        ajax(`/games/${getGameId()}/status`, {},  (newStatus) => {
            this.setState(() => (newStatus), () => {
                //Pull the status only if the game is not over
                if (newStatus.game.status != "failed" && newStatus.game.status != "won"){
                    setTimeout(() => {this.gameLoop()}, 2000);
                } 
             });
        });
    }

    isViewMode(){
        return this.state.user.status == "viewer" && (this.state.game.status === "on" || this.state.players.length == STEPS);
    }

    render() {
        return <div className="main">
                <div className="center">
                    <BackBtn></BackBtn>
                    <Simon  sequence={this.state.game.sequence} disabled={this.state.user.status != "turn"} showPlayBtn={this.state.user.status == "new"}/>
                    <Modal players={this.state.players.filter(player => player["status"] == this.state.game.status)} outcome={this.state.game.status} />
                    <Sequence sequence={this.state.game.sequence} step={this.state.game.step} />
                </div>
                <div className="side">
                    <div className="game-name">{this.state.game.name}</div>
                    {(this.isViewMode()) && <div className="view-mode" >View mode</div>}
                    <div className={`game-status ${this.state.game.status}`}>{this.state.game.status}</div>
                    <Players players={this.state.players} userName={this.state.user.name} showJoinBtn={ this.state.user.status == "viewer" && this.state.game.status === "open"} />
                </div>
            </div>
    }
}