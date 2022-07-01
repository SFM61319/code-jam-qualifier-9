import typing
import dataclasses


@dataclasses.dataclass(frozen=True)
class Request:
    scope: typing.Mapping[str, typing.Any]

    receive: typing.Callable[[], typing.Awaitable[object]]
    send: typing.Callable[[object], typing.Awaitable[None]]


class RestaurantManager:
    def __init__(self):
        """
        Instantiate the restaurant manager.

        This is called at the start of each day before any staff get on
        duty or any orders come in. You should do any setup necessary
        to get the system working before the day starts here; we have
        already defined a staff dictionary.
        """

        self.staff: dict[str, Request] = {}

    async def __call__(self, request: Request):
        """
        Handle a request received.

        This is called for each request received by your application.
        In here is where most of the code for your system should go.

        :param request: request object
            Request object containing information about the sent
            request to your application.
        """

        match request.scope["type"]:
            case "staff.onduty":
                await self.__login_staff(request)

            case "staff.offduty":
                await self.__logout_staff(request)

            case "order":
                await self.__handle_order(request)

    async def __login_staff(self, request: Request):
        """
        Log in a staff member.

        This function adds the member's *Request* to
        the *staff* dictionary by the member's staff ID.

        :param Request request:
            Request object containing information about the sent
            request to your application.
        """

        self.staff[request.scope["id"]] = request

    async def __logout_staff(self, request: Request):
        """
        Log out a staff member.

        This function removes the member's *Request* from
        the *staff* dictionary by the member's staff ID.

        :param Request request:
            Request object containing information about the sent
            request to your application.
        """

        del self.staff[request.scope["id"]]

    async def __handle_order(self, request: Request):
        """
        Handle users' orders.

        This function takes in users' orders, sends them to the staff, receives
        the prepared food from the staff, and delivers them to the users.

        :param Request request:
            Request object containing information about the sent
            request to your application.
        """

        chef: Request = None

        for chef in self.staff.values():
            if request.scope["speciality"] in chef.scope["speciality"]:
                break

        full_order = await request.receive()
        await chef.send(full_order)

        food = await chef.receive()
        await request.send(food)
