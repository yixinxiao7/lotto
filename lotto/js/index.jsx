import React from 'react';
import ReactDOM from 'react-dom';

import Result from './result';


class Index extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            results: [],  //list of strs
            text: '',
            dateText: '',
            yearText: '',
            displayText: '',
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleFileSubmit = this.handleFileSubmit.bind(this);
        this.handleClick = this.handleClick.bind(this);
        this.renderResults = this.renderResults.bind(this);
        this.handlePrediction = this.handlePrediction.bind(this);
    }

    handleSubmit(event) {
        /* POST request */
        event.preventDefault();
        const url = '/api/';
        const data = JSON.stringify({year: this.state.yearText,
                                     date: this.state.dateText,
                                     text: this.state.text
                                    });
        fetch(url, { 
            method: 'POST',
            credentials: 'include',
            headers: {
                'Accept': 'application/json',
                'Content-Type':  'application/json',
            },
            body: data })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .then((data) => {  // combination added
                console.log(data.model);
                alert('Entry added');
            })
            .catch(error => console.log(error));
    }

    handleFileSubmit(e) {
        e.preventDefault();
        // data info: e.target.result
        let files = e.target.files;
        let reader = new FileReader();
        reader.readAsDataURL(files[0]);
        reader.onload = function(event) {
            // console.log(event.target.result);
            const url = '/excelupload/';
            const data = JSON.stringify({file: event.target.result});
            fetch(url, { 
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type':  'application/json',
                },
                body: data })
                .then((response) => {
                    if (!response.ok) throw Error(response.statusText);
                    return response.json();
                })
                .then((data) => {
                    alert('File uploaded');
                })
                .catch(error => console.log(error));
            };
    }

    handleClick(event){
        /* GET request */
        event.preventDefault();
        const url=`/api/?size=${this.state.displayText}`;
        fetch(url, { credentials: 'same-origin' })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .then((data) => {
                let dataResults = [];
                let entry = '';
                for (let i = 0; i < data.entries.length; i += 1) {
                    //  dict object
                    entry = entry.concat(
                                 data.entries[i].year, ': ',
                                 data.entries[i].date, ': ',
                                 data.entries[i].val1, ' ',
                                 data.entries[i].val2, ' ',
                                 data.entries[i].val3, ' ',
                                 data.entries[i].val4, ' ',
                                 data.entries[i].val5, ' ',
                                 data.entries[i].model, ' ',
                                 data.entries[i].model_ranges,
                    );
                    dataResults.push(entry);

                    //reset entry
                    entry = '';
                }
                this.setState({
                    results: dataResults,
                });
            });
    }

    renderResults() {
        const {results} = this.state;
        const resultsList = [];
        if (results.length !== 0) {
            for (let i = 0; i < results.length; i += 1) {
                resultsList.push(
                    <Result
                        text={results[i]}
                    />,
                )
            }
        }
        return resultsList;
    }

    handlePrediction(event){
        /* GET */
        // event.preventDefault();
        console.log(event);
        const url='/prediction/';
        fetch(url, { credentials: 'same-origin' })
            .then((response) => {
                if (!response.ok) throw Error(response.statusText);
                return response.json();
            })
            .then((data) => {
                alert(`Model: ${data.model}`);
            });
    }

    render() {
        return(
            <div>
                <form onSubmit={this.handleSubmit}>
                    <p>
                        <b>Year &nbsp;</b>
                        <input
                            type="text"
                            name="year_input"
                            value={this.state.yearText}
                            onChange={(e) => this.setState({ yearText: e.target.value })}
                        />
                    </p>
                    <p>
                        <b>Occurrence &nbsp;</b>
                        <input
                            type="text"
                            name="date_input"
                            value={this.state.dateText}
                            onChange={(e) => this.setState({ dateText: e.target.value })}
                        />
                    </p>
                    <p>
                        <b>Combination &nbsp;</b>
                        <input
                            type="text"
                            name="text_input"
                            value={this.state.text}
                            onChange={(e) => this.setState({ text: e.target.value })}
                        />
                        <input
                            type="submit"
                            value="Submit"
                        />
                    </p>
                </form>
                <br/>
                <div onSubmit={this.onFormSubmit}>
                    <p><b>Upload excel file data</b></p>
                    <input 
                        type="file"
                        name="file"
                        onChange={(e) => this.handleFileSubmit(e)}
                    />
                </div>
                <br/>
                <br/>
                <button onClick={this.handlePrediction}>
                    Make Prediction
                </button>
                <br/>
                <br/>
                <p><b>Show database</b></p>
                <form onSubmit={this.handleClick}>
                    <input
                        type="text"
                        name="result_opt"
                        value={this.state.displayText}
                        onChange={(e) => this.setState({ displayText: e.target.value })}
                    />
                    <input
                        type="submit"
                        value="Show Entries"
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
