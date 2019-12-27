import React from 'react';
import PropTypes from 'prop-types';

class Result extends React.Component {
  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = {};
  }

  render() {
    const { text } = this.props;
    return (
      <div>
          <p>{text}</p>
      </div>
    );
  }
}

Result.propTypes = {
  text: PropTypes.string.isRequired,
};

export default Result;
