import React from 'react';
import '../../css/modal.css';

export default class Modal extends React.Component {
    render() {
        return (
            <div id="myModal" className="modal fade" role="dialog">
                <div className="modal-dialog">
                    <div className={`modal-content ${this.props.outcome}`}>
                        <div className="modal-header">
                            {this.props.outcome == "won" && <h3>Congratulations!</h3>}
                            <button type="button" className="close" data-dismiss="modal">&times;</button>
                        </div>
                        <div className="modal-body">
                            {this.props.outcome == "won" && <p>{this.props.players.map(k => (
                                <span key={k.player}>{k.player} </span>
                            ))} won!!!</p>}
                        </div>
                        {this.props.outcome == "won" && <div className="modal-footer">
                            <button type="button" className="btn btn-default" data-dismiss="modal">Close</button>
                        </div>}
                    </div>

                </div>
            </div>
        );
    }
}