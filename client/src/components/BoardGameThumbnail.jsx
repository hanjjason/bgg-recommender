import React, { Component} from 'react';

class BoardGameThumbnail extends Component{
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className='thumbnail' >
        <img src={this.props.game.image} height='250' onClick={this.props.toggleModal.bind(this,this.props.game)} />
        <div>{this.props.game.name}</div>
      </div>
    )
  }
}

export default BoardGameThumbnail;