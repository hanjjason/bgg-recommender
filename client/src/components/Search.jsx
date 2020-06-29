import React, { Component} from 'react';

class Search extends Component{
  constructor(props) {
    super(props);

    this.state = {
      searchTerm: '',
    }

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({searchTerm: event.target.value});
  }

  handleSubmit(event) {
    event.preventDefault();
    this.props.changeActiveUser(this.state.searchTerm);
  }

  render() {
    return(
      <div className='Search'>
        <form onSubmit={this.handleSubmit}>
          <label>
            BGG Username:
            <input type='text' value={this.state.searchTerm} onChange={this.handleChange} />
          </label>
          <input type='submit' value='Submit' />
        </form>
      </div>
    );
  }
}

export default Search;