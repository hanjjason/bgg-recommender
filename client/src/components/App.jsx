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

  fetchData() {
    axios.get(`/api/user/${this.state.username}`)
      .then((data) => (this.setState({
        'data': data
      })));
  }

  changeActiveUser(user) {
    this.setState({
      'username': user
    });
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