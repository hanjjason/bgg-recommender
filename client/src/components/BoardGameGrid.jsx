import React, { Component} from 'react';
import BoardGameThumbnail from './BoardGameThumbnail.jsx'

class BoardGameGrid extends Component{
  constructor(props) {
    super(props);
  }

  render() {
    let boardGames = this.props.data.map((game) => {
      return <BoardGameThumbnail game={game} toggleModal={this.props.toggleModal} key={game.id} />
    })
    return (
      <div className='grid'>
        {boardGames}
      </div>
    );
  }
}

export default BoardGameGrid;