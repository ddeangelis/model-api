<p align="center">
<a href="https://tycherisk.co"><img src="tyche_logo.png" alt="Tyche"></a><br/>
<b>A web service for calculating, recording, and delivering predictive model inferences via API.</b><br/>
</p>

Tyche builds predictive models for the insurance industry. We maintain those models and deliver inferences on-demand via web API. This repository is the API product that houses predictive models. In this example, the model is a submission binding model for a commercial general liability insurance carrier. The model itself is represented as a [Scikit-Learn](http://scikit-learn.org) random forest classifier serialized in set of PKL files. The model itself and the code to generate the model contain proprietary information and are not included in this repository. However, this source code can be easily adapted to track and deliver model inferences from any arbitrary model. This API product has been tailored to run on [Google App Engine](https://cloud.google.com/appengine/).

**Note:** The submission binding model PKL files and generating source are not included in this repository.

## API Documentation
HTML format documentation of the API (and model) functionality is located in the `/api_docs` directory. This was generated using [Spectacle](https://github.com/sourcey/spectacle) from an [OpenAPI 2.0](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md) specification file, `tyche_api.yaml`. 

## Folder Structure
```bash
.
├── api_docs
│   ├── Insurance Submission Binding Model API | API Reference_files
│   │   ├── foundation.css
│   │   ├── jquery-2.js
│   │   ├── spectacle.css
│   │   ├── spectacle.js
│   │   └── tyche-gmail-logo.png
│   └── Insurance Submission Binding Model API | API Reference.html
├── app.yaml
├── blank_model_stubs
│   ├── blank_model_stub.py
│   ├── __init.py__
│   └── model_stub.py
├── client_examples
│   ├── curl_examples.txt
│   ├── python_examples.txt
│   └── sample_submission.json
├── config_template.json
├── LICENSE
├── main.py
├── README.md
├── requirements.txt
├── tyche_api.yaml
├── tyche_binding_model
│   ├── __init.py__
│   ├── jr_mca.py
│   ├── jr_model_stub.py
│   ├── jr_utils.py
│   └── jr_wildcat.py
├── tyche_db.py
└── tyche_logo.png
```

`tyche_binding_model/` contains truncated utility and wrapper functions that are necessary to load the model PKL files and draw inferences. 

## Example usage

`client_examples/` contains usage examples, in Python and command-line curl. 
