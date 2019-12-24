import React from 'react';
import ReactDOM from 'react-dom';


class Index extends React.Component {
    consructor(props) {
        super(props);
        this.state = {
            results: [],
            text: '',
            dateText: '',
        };
        this.renderResults = this.renderResults.bind(this);
        
    }

    handleSubmit(event) {
        /* POST request */
        event.preventDefault();
        const url = '/api/'
        const data = JSON.stringify({date: this.state.dateText, text: this.state.text});

        fetch(url, { 
            method: 'POST',
            credentials: 'include',
            headers: {
                Accept: 'application/json',
                'Content-Type':  'application/json',
            },
            body: data })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .then((data) => {  // combination added
                console.log(data);
            })
            .catch(error => console.log(error));
    }

    renderResults() {
        const resultsList = [];
        if (results.length !== 0) {
            for (let i = 0; i < results.length; i += 1) {
                resultsLists.push(
                    //TODO: IMPLEMENT
                )
            }
        }
    }

    render() {
        return(
            <div>
                <form onSubmit={this.handleSubmit}>
                    <b>Date</b>
                    <input
                        type="text"
                        name="date_input"
                        value={dateText}
                        onChange={(e) => this.setState({ dateText: e.target.value })}
                    />
                    <b>Combination</b>
                    <input
                        type="text"
                        name="text_input"
                        value={text}
                        onChange={(e) => this.setState({ text: e.target.value })}
                    />
                    <input
                        type="submit"
                        value="Submit"
                    />
                </form>
                <div>
                    {this.renderResults()}
                </div>
            </div>
        )
    }
    
}

ReactDOM.render(
    <Index/>,
    document.getElementById('reactEntry'),
)