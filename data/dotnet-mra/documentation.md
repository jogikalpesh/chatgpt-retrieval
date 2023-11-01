# .NET Microservice Reference Architecture

## 1. Logical Structure

### 1.1 Overview
This REST API-based microservice follows a 3-tier architecture. The first layer comprises controllers, the second layer consists of business services, and the third layer contains repositories for database interactions.

### 1.2 Layer Details
1. **Controllers Layer**: This layer contains all the controllers and middleware components.
2. **Business Layer**: All business logic and validation are handled in this layer.
3. **Repository Layer**: This layer is responsible for all database interactions and includes repository classes, typically one per collection in the MongoDB database.

### 1.3 Loose Coupling
The code is structured to promote loose coupling following Dependency Inversion principles.

### 1.4 Gateway Classes
For integrating with other microservices or third-party components, gateway classes are used. Business services communicate with these gateways, ensuring loose coupling between services and gateways.

### 1.5 Validation
Validation is performed using the FluentValidator Library.

## 2. Unit Testing

### 2.1 Testing Scope
Unit testing is carried out for the following components:
- Controllers
- Business services
- Validators

### 2.2 Architectural Pattern
Unit tests follow the "Arrange, Act, and Assert" architectural pattern.

### 2.3 Dependency Injection
Dependency injection enables the mocking of dependent components during unit testing.

### 2.4 Mocking Framework
Unit testing utilizes the NSubstitute library for mocking.

### 2.5 Assertion Framework
Assertions are made using the Shouldly library.

## 3. Code Structure

### 3.1 Class Libraries
The project is structured using two sets of class libraries: one for the code and another for unit tests.

### 3.2 Libraries Details
1. **Controller Class Library**: This library is a WebAPI 2 project that contains all controllers, filters, and middlewares.
2. **Business Service Class Library**: This class library includes business services (and their corresponding interfaces), validators, and gateways (along with their interfaces).
3. **Repository Class Library**: This class library follows the repository pattern and contains classes corresponding to each collection in the MongoDB database.
4. **Entity Library**: This is a simple class library containing all business entities.

### 3.3 References
- The Controller library references the Business Service and Entity class libraries.
- The Business Service library references the Repository and Entity class libraries.
- The Repository library references the Entity class library.

### 3.4 Dependency Injection Configuration
On startup, a dependency container is initialized. Installer classes are present in each of the class libraries to add dependencies to the DI container.
   - The Controller library's installer class adds its dependencies and then calls the installer class in the Business Service library.
   - The Business Service installer adds its dependencies and then calls the installer in the Repository library.
   - Installer classes use the Scrutor library to automatically discover dependencies and add them to the DI container.

This structure facilitates clean separation of concerns, promotes testability, and enables flexible scaling of your microservice.

This documentation provides an overview of your .NET microservice architecture, its logical structure, unit testing approach, and code organization. It serves as a valuable resource for developers working on the project.

### 3.5 Folder Structure

This is Folder structure for Boilerplate code for dotnet based Rest API. 

APIInstaller: Uses scrutor to scan through entire api layer and adds all the controllers in dependency container.
ServiceInstaller: Uses scrutor to scan through entire service layer and adds all the services, Gateways and Validators in dependency container.
DataInstaller: Uses scrutor to scan through entire Data layer and adds all the repositories in dependency container.

<pre>
ProjectName/
┣ Code/
┃ ┣ ProjectName.Api/
┃ ┃ ┣ Controllers/
┃ ┃ ┃ ┗ SampleController.cs
┃ ┃ ┣ Filters/
┃ ┃ ┃ ┗ HttpResponseExceptionFilter.cs
┃ ┃ ┣ Installer/
┃ ┃ ┃ ┗ APIInstaller.cs
┃ ┃ ┣ Middleware/
┃ ┃ ┃ ┗ RequestResponseLoggingMiddleware.cs
┃ ┃ ┣ appsettings.Development.json
┃ ┃ ┣ appsettings.json
┃ ┃ ┣ ProjectName.Api.csproj
┃ ┃ ┣ nlog.config
┃ ┃ ┣ Program.cs
┃ ┃ ┗ Startup.cs
┃ ┣ ProjectName.Business/
┃ ┃ ┣ Installer/
┃ ┃ ┃ ┗ ServiceInstaller.cs
┃ ┃ ┣ Interfaces/
┃ ┃ ┃ ┗ ISampleService.cs
┃ ┃ ┣ Services/
┃ ┃ ┃ ┗ SampleService.cs
┃ ┃ ┗ ProjectName.Business.csproj
┃ ┣ ProjectName.Data/
┃ ┃ ┣ Installer/
┃ ┃ ┃ ┗ DataInstaller.cs
┃ ┃ ┣ Interfaces/
┃ ┃ ┃ ┣ IDelete.cs
┃ ┃ ┃ ┣ IGetAll.cs
┃ ┃ ┃ ┣ IGetById.cs
┃ ┃ ┃ ┣ ISampleRepository.cs
┃ ┃ ┃ ┣ ISave.cs
┃ ┃ ┃ ┗ IUpdate.cs
┃ ┃ ┣ Repositories/
┃ ┃ ┃ ┣ DataContext.cs
┃ ┃ ┃ ┗ SampleRepository.cs
┃ ┃ ┗ ProjectName.Data.csproj
┃ ┣ ProjectName.Entities/
┃ ┃ ┣ Entities/
┃ ┃ ┃ ┗ Sample.cs
┃ ┃ ┗ ProjectName.Entities.csproj
┃ ┣ ProjectName.Test.Api/
┃ ┃ ┣ SampleControllerSpec/
┃ ┃ ┃ ┣ UsingSampleControllerSpec.cs
┃ ┃ ┃ ┣ When_deleting_sample.cs
┃ ┃ ┃ ┣ When_getting_all_samples.cs
┃ ┃ ┃ ┣ When_saving_sample.cs
┃ ┃ ┃ ┗ When_updating_sample.cs
┃ ┃ ┗ ProjectName.Test.Api.csproj
┃ ┣ ProjectName.Test.Business/
┃ ┃ ┣ SampleServiceSpec/
┃ ┃ ┃ ┣ UsingSampleServiceSpec.cs
┃ ┃ ┃ ┣ When_deleting_sample.cs
┃ ┃ ┃ ┣ When_getting_all_sample.cs
┃ ┃ ┃ ┣ When_saving_sample.cs
┃ ┃ ┃ ┗ When_updating_sample.cs
┃ ┃ ┗ ProjectName.Test.Business.csproj
┃ ┣ ProjectName.Test.Framework/
┃ ┃ ┣ ProjectName.Test.Framework.csproj
┃ ┃ ┗ SpecFor.cs
┃ ┗ .gitignore
┣ .dockerignore
┣ ProjectName.sln
┣ Dockerfile.build
┗ Dockerfile.publish
</pre>