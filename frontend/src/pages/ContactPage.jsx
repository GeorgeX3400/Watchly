import React, { useState } from 'react';

const ContactPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    surname: '',
    birthdate: '',
    email: '',
    confirm_email: '',
    message_type: '',
    subject: '',
    min_wait_days: 1,
    message: ''
  });

  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);

    // Validation
    const formErrors = validateForm(formData);
    if (Object.keys(formErrors).length > 0) {
      setErrors(formErrors);
      setIsSubmitting(false);
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/contact/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        alert('Message sent successfully!');
        setFormData({
          name: '',
          surname: '',
          birthdate: '',
          email: '',
          confirm_email: '',
          message_type: '',
          subject: '',
          min_wait_days: 1,
          message: ''
        });
      } else {
        alert('Something went wrong. Please try again.');
      }
    } catch (error) {
      console.error('Error submitting the form:', error);
      alert('There was an error submitting the form.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const validateForm = (data) => {
    const formErrors = {};
    if (!data.name) formErrors.name = 'Name is required';
    if (data.email !== data.confirm_email) formErrors.confirm_email = 'Emails do not match';
    if (data.message && (data.message.split(' ').length < 5 || data.message.split(' ').length > 100)) {
      formErrors.message = 'Message must contain between 5 and 100 words';
    }
    if (data.message.includes('http://') || data.message.includes('https://')) {
      formErrors.message = 'Message cannot contain links';
    }
    if (data.message && !data.message.trim().endsWith(data.name)) {
      formErrors.message = 'Message must end with your name as a signature';
    }
    if (data.birthdate) {
      const birthdate = new Date(data.birthdate);
      const age = new Date().getFullYear() - birthdate.getFullYear();
      if (age < 18) formErrors.birthdate = 'You must be at least 18 years old';
    }

    return formErrors;
  };

  return (
    <div className="contact-form-container">
      <h2>Contact Us</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Name</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Name"
          />
          {errors.name && <p className="error">{errors.name}</p>}
        </div>

        <div className="form-group">
          <label htmlFor="surname">Surname</label>
          <input
            type="text"
            id="surname"
            name="surname"
            value={formData.surname}
            onChange={handleChange}
            placeholder="Surname"
          />
        </div>

        <div className="form-group">
          <label htmlFor="birthdate">Date of Birth</label>
          <input
            type="date"
            id="birthdate"
            name="birthdate"
            value={formData.birthdate}
            onChange={handleChange}
          />
          {errors.birthdate && <p className="error">{errors.birthdate}</p>}
        </div>

        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="Email"
          />
        </div>

        <div className="form-group">
          <label htmlFor="confirm_email">Confirm Email</label>
          <input
            type="email"
            id="confirm_email"
            name="confirm_email"
            value={formData.confirm_email}
            onChange={handleChange}
            placeholder="Confirm Email"
          />
          {errors.confirm_email && <p className="error">{errors.confirm_email}</p>}
        </div>

        <div className="form-group">
          <label htmlFor="message_type">Message Type</label>
          <select
            id="message_type"
            name="message_type"
            value={formData.message_type}
            onChange={handleChange}
          >
            <option value="reclamatie">Complaint</option>
            <option value="intrebare">Question</option>
            <option value="review">Review</option>
            <option value="cerere">Request</option>
            <option value="programare">Appointment</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="subject">Subject</label>
          <input
            type="text"
            id="subject"
            name="subject"
            value={formData.subject}
            onChange={handleChange}
            placeholder="Subject"
          />
        </div>

        <div className="form-group">
          <label htmlFor="min_wait_days">Minimum Wait Days</label>
          <input
            type="number"
            id="min_wait_days"
            name="min_wait_days"
            value={formData.min_wait_days}
            onChange={handleChange}
            min="1"
          />
        </div>

        <div className="form-group">
          <label htmlFor="message">Message</label>
          <textarea
            id="message"
            name="message"
            value={formData.message}
            onChange={handleChange}
            placeholder="Type your message here..."
          />
          {errors.message && <p className="error">{errors.message}</p>}
        </div>

        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Submitting...' : 'Submit'}
        </button>
      </form>
    </div>
  );
};

export default ContactPage;
