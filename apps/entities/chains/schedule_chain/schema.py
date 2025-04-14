from pydantic import BaseModel, Field
from datetime import datetime, timedelta


class ReadCommandModel(BaseModel):
    """
    Represents a command model for reading scheduled events.

    This model allows filtering of schedule events based on a time range.
    It includes a flag to enable the read operation and optional filters
    for start and end times.

    Attributes:
        flag (bool): Whether to perform a read operation.
        time_max (datetime): The latest possible start time for events to include in the result.
        time_min (datetime): The earliest possible end time for events to include in the result.
    """

    flag: bool = Field(
        default=False, description="Indicates whether to perform a read operation."
    )
    time_max: datetime = Field(
        default_factory=datetime.now,
        description="The latest start time of events to include in the result.",
    )
    time_min: datetime = Field(
        default_factory=datetime.now,
        description="The earliest end time of events to include in the result.",
    )


from enum import Enum


class EventTypes(str, Enum):
    birthday: str = "birthday"  # 생일
    default: str = "default"  # 기본 일정
    focusTime: str = "focusTime"  # 집중 시간
    outOfOffice: str = "outOfOffice"  # 부재 중


class StartTime(BaseModel):
    dateTime: datetime = Field(
        default=datetime.now(), description="The start time of the event."
    )
    timeZone: str = Field(
        default="Asia/Seoul", description="The time zone of the event."
    )


class EndTime(BaseModel):
    dateTime: datetime = Field(
        default=datetime.now(), description="The end time of the event."
    )
    timeZone: str = Field(
        default="Asia/Seoul", description="The time zone of the event."
    )


class RegisterCommandModel(BaseModel):
    """
    Represents a command model for registering a new scheduled event.

    This model encapsulates all required information for schedule registration,
    including the type, timing, and metadata of the event.

    Attributes:
        flag (bool): Whether to perform a register operation.
        summary (str): A short title or summary of the event.
        description (str): A detailed explanation of the event.
        location (str): The location where the event will take place.
        event_type (EventTypes): The category of the event (e.g., birthday, focusTime).
        start (datetime): The start time of the event.
        interval (int): The duration of the event in hours.
    """

    flag: bool = Field(
        default=False, description="Indicates whether to perform a register operation."
    )
    summary: str = Field(
        default="", description="A short title or summary of the event."
    )
    description: str = Field(
        default="", description="A detailed explanation or notes about the event."
    )
    location: str = Field(
        default="", description="The location where the event will take place."
    )
    event_type: EventTypes = Field(
        default=EventTypes.default,
        description="The category of the event (e.g., birthday, focusTime).",
    )
    start: StartTime = Field(
        default=datetime.now(),
        description="The start time information about the event.",
    )
    end: EndTime = Field(
        default=datetime.now() + timedelta(hours=1),
        description="The end time information about the event. default is 1 hour later from start   ",
    )
    interval: int = Field(
        default=60, description="The duration of the event in minutes"
    )


class DeleteCommandModel(BaseModel):
    """
    Represents a model for a delete command.

    This class is designed to be used for defining and validating
    the structure of data associated with delete commands.
    It extends the BaseModel to leverage validation and data modeling functionality.
    """

    pass


class UpdateCommandModel(BaseModel):
    """
    Represents a model for update command operations.

    This class is designed to serve as a data model for handling update commands
    within a specific context, utilizing BaseModel features from Pydantic. It
    guarantees structured data validation and other related functionalities. This
    model is intended for internal use in scenarios that require update operations.
    """

    pass


class ScheduleCommandModel(BaseModel):
    """
    Represents a container for scheduling commands including read and register commands.

    This class is a data model used for managing scheduling commands by encapsulating
    read and register command models. It extends the functionality of BaseModel from
    Pydantic and is intended to provide structured and validated data when working
    with command-related operations.

    Attributes:
    read_command (ReadCommandModel): Represents the model for a read command.
    register_command (RegisterCommandModel): Represents the model for a register
    command.
    """

    read_command: ReadCommandModel = Field(description="read schedule command")
    register_command: RegisterCommandModel = Field(
        description="register schedule command"
    )
