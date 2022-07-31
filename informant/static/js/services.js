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

function setupTeacher(data) {
    return {
        id: data.id,
        fio: data.fio,
        participation_period: data.participation_period,
        mounth: data.mounth,
        level: data.level,
        category: data.category,
        sub_category: data.sub_category,
        document: data.category_document,
        result: data.result,
        kpk: data.kpk__id,
        kpk_document: data.kpk_document,
        publications_name: data.publications__name,
        publications_name_journal: data.publications__name_journal,
        publications_city: data.publications__city,
        publications_page_range: data.publications__page_range,
        publications_document: data.publications_document,
    }
}

function setupKPK(data) {
    return {
        id: data.id,
        kpk_name: data.kpk__name,
        kpk_city: data.kpk__city,
        kpk_organization: data.kpk__organization,
        kpk_date_issue: data.kpk__date_issue,
        kpk_number_hours: data.kpk__number_hours,
    }
}

function setupKPKUpdate(data) {
    return {
        id: data.id,
        kpk_name: data.name,
        kpk_city: data.city,
        kpk_organization: data.organization,
        kpk_date_issue: data.date_issue,
        kpk_number_hours: data.number_hours,
    }
}