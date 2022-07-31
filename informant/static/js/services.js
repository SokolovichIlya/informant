function setupStudent(data) {
    return {
        id: data.id,
        fio: data.fio,
        participation_period: data.participation_period,
        mounth: data.mounth,
        level: data.level,
        category: data.category_id,
        sub_category: data.sub_category_id,
        document_link: data.document,
        teacher: data.teacher_id,
        result: data.result,
        participation_in_profile_shifts: data.participation_in_profile_shifts_id,
        name_program: data.name_program,
    }
}