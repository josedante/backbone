# Backbone

#### The foundation of a natively digital business.

Backbone is a Django project that contains a set of applications and some pre set configuration files intended to shorten the time to market of your Backbone project.

We view Backbone -as its name suggests- as a neural center for your business. It will collect and organize your customers information guided by the thread that makes most sense: the customer's lifecycle as defined by the series of interactions that they have with your company along the diverse touchpoints it offers.

There will be two ways to feed information to Backbone. You will either send customer interaction data through a REST API, or you will have an integrated django application such as a website that captures information directly to Backbone.

## Applications

There are three types of applications in **Backbone**: Core Backbone Applications, Connective Sample Applications, and Periferal Sample Applications.

### Core Backbone Applications

These applications aim to be the neural center of your business. Most importantly the *Lifecycle Application*.

### Connective Sample Applications

These applications intend to show you how Backbone will be able to connect with periferal systems that live outside your project such as Location Beacons.

### Periferal Sample Applications

These are the applications that inject life to the interactions with your customers while at the same time feed information to you Backbone project.

## Configuration

The configuration decisions that have been made aim to facilitate the publication of your Backbone project on the infraestructure of Amazon Web Services.

Most importantly, the settings file expects a series of environment variables that will allow you to work independently and without trouble in a local, development, staging and production environments.

These are the required environment variables:

```python
export DEBUG='true'
export SECRET_KEY='SECRET_KEY'
export S3_BUCKET_NAME='S3_BUCKET_NAME'
export S3_KEY_ID='S3_KEY_ID'
export S3_ACCESS_KEY='S3_ACCESS_KEY'
export RDS_DB_NAME='RDS_DB_NAME'
export RDS_USERNAME='RDS_USERNAME'
export RDS_PASSWORD='RDS_PASSWORD'
export RDS_HOSTNAME='RDS_HOSTNAME'
export RDS_PORT='3306'
```