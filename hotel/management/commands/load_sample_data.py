from django.core.management.base import BaseCommand
from hotel.models import RoomType, Room

class Command(BaseCommand):
    help = 'Load sample data for the hotel'

    def handle(self, *args, **kwargs):
        # Create room types
        room_types_data = [
            {
                'name': 'Standard Room',
                'description': 'Comfortable room with all basic amenities, perfect for solo travelers or couples.',
                'price_per_night': 99.00,
                'capacity': 2
            },
            {
                'name': 'Deluxe Room',
                'description': 'Spacious room with premium amenities and beautiful city views.',
                'price_per_night': 149.00,
                'capacity': 3
            },
            {
                'name': 'Executive Suite',
                'description': 'Luxurious suite with separate living area and premium services.',
                'price_per_night': 249.00,
                'capacity': 4
            },
            {
                'name': 'Presidential Suite',
                'description': 'The ultimate luxury experience with panoramic views and exclusive amenities.',
                'price_per_night': 499.00,
                'capacity': 6
            }
        ]

        for data in room_types_data:
            room_type, created = RoomType.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created room type: {room_type.name}')

        # Create rooms
        rooms_data = [
            ('101', 'Standard Room'),
            ('102', 'Standard Room'),
            ('103', 'Standard Room'),
            ('201', 'Deluxe Room'),
            ('202', 'Deluxe Room'),
            ('301', 'Executive Suite'),
            ('401', 'Presidential Suite'),
        ]

        for room_number, room_type_name in rooms_data:
            room_type = RoomType.objects.get(name=room_type_name)
            room, created = Room.objects.get_or_create(
                room_number=room_number,
                defaults={'room_type': room_type}
            )
            if created:
                self.stdout.write(f'Created room: {room.room_number}')

        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))