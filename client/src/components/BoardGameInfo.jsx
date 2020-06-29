import React, { Component} from 'react';

class BoardGameInfo extends Component{
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="modal" id="modal">
        <h2>{this.props.game.name}</h2>
        <div className="content">{this.props.game.description}</div>
        <div className="actions">
          <button className="toggle-button" onClick={this.props.toggleModal}>
            Close
          </button>
        </div>
      </div>
    );
  }
}

export default BoardGameInfo;