import React from "react";

export default class BackBtn extends React.Component {
    render() {
        return (
            <a id="back" href="/start">
                <div className="arrow" id="arrow-head"></div>
                <div className="arrow" id="arrow-body"></div>
            </a>
        );
    }
}