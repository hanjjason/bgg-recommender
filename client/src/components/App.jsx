import React, { Component} from 'react';
import axios from 'axios';

import Search from './Search.jsx';
import BoardGameGrid from './BoardGameGrid.jsx';
import BoardGameInfo from './BoardGameInfo.jsx';

class App extends Component{
  constructor(props) {
    super(props);

    this.state = {
      username: '',
      data: [],
      modalActive: false,
      currentBoardGame: {}
    }

    this.changeActiveUser = this.changeActiveUser.bind(this);
    this.toggleModal = this.toggleModal.bind(this);
  }

  componentDidMount() {
    axios.get('/api/top10')
      .then((results) => (this.setState({
        data: results.data.data
      })));
  }

  changeActiveUser(user) {
    axios.get(`/api/recommend/${user}`)
      .then((results) => (this.setState({
        'username': user,
        'data': results.data.data
      })));
  }

  toggleModal(game) {
    let temp = false;
    if (!this.state.modalActive) {
      temp = true;
    }
    this.setState({
      'modalActive': temp,
      'currentBoardGame': game
    })
  }

  render() {
    return(
      <div className='App'>
        <h1> Board Game Recommender! </h1>
        <Search changeActiveUser={this.changeActiveUser} />
        {this.state.username !== '' && <div> Results for {this.state.username} </div>}
        <BoardGameGrid data={this.state.data} toggleModal={this.toggleModal} />
        {this.state.modalActive && <BoardGameInfo game={this.state.currentBoardGame} toggleModal={this.toggleModal} />}
      </div>
    );
  }
}

export default App;